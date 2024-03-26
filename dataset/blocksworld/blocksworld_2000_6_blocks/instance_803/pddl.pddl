

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(ontable c)
(on d e)
(on e c)
(clear a)
(clear b)
(clear d)
)
(:goal
(and
(on a d)
(on d c)
(on e a))
)
)


