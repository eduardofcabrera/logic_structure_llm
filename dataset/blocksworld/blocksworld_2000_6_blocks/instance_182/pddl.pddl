

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(ontable c)
(ontable d)
(on e d)
(clear a)
(clear c)
(clear e)
)
(:goal
(and
(on a c)
(on b e)
(on c d)
(on d b))
)
)


