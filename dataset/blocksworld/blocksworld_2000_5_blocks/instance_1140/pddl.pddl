

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(ontable b)
(ontable c)
(on d b)
(on e a)
(clear c)
(clear e)
)
(:goal
(and
(on c a)
(on d e))
)
)


