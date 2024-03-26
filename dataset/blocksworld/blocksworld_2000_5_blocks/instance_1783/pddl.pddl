

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(ontable b)
(ontable c)
(on d b)
(on e d)
(clear a)
(clear c)
)
(:goal
(and
(on c e)
(on d b)
(on e d))
)
)


