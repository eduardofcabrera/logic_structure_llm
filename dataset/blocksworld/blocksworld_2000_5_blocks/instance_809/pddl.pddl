

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b c)
(ontable c)
(on d b)
(on e a)
(clear d)
(clear e)
)
(:goal
(and
(on a e)
(on b a)
(on c d))
)
)


