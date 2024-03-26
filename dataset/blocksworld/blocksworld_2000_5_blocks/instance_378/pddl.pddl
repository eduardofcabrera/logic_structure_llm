

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(ontable c)
(ontable d)
(on e c)
(clear b)
(clear d)
(clear e)
)
(:goal
(and
(on b e)
(on c d)
(on d b))
)
)


